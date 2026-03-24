#!/usr/bin/env python3

import subprocess
import sys
import os
from typing import List, Optional

class GitMutator:
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        if not os.path.exists(os.path.join(repo_path, '.git')):
            raise ValueError(f'Not a git repository: {repo_path}')

    def _run_git(self, cmd: List[str]) -> str:
        """Execute git command and return output"""
        result = subprocess.run(
            ['git'] + cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f'Git command failed: {result.stderr}')
        return result.stdout.strip()

    def is_clean_workspace(self) -> bool:
        """Check if working directory is clean"""
        return not bool(self._run_git(['status', '--porcelain']))

    def current_branch(self) -> str:
        """Get name of current branch"""
        return self._run_git(['rev-parse', '--abbrev-ref', 'HEAD'])

    def mutate_branch(self, source_branch: str, mutation_count: int = 1) -> str:
        """Create a new branch with random mutations from source"""
        if not self.is_clean_workspace():
            raise RuntimeError('Working directory must be clean')

        # Create new branch name
        new_branch = f'mutated_{source_branch}_{mutation_count}'
        
        # Create new branch from source
        self._run_git(['checkout', '-b', new_branch, source_branch])

        try:
            # Get list of files in repo
            files = self._run_git(['ls-files']).splitlines()
            
            # TODO: Implement actual mutation logic here
            # For now just touch files to demonstrate structure
            for _ in range(mutation_count):
                if files:
                    target = files[0]
                    with open(os.path.join(self.repo_path, target), 'a') as f:
                        f.write('\n# Mutation placeholder\n')

            # Commit changes
            self._run_git(['add', '-A'])
            self._run_git(['commit', '-m', f'feat: mutation round {mutation_count}'])
            
            return new_branch

        except Exception as e:
            # Cleanup on failure
            self._run_git(['checkout', source_branch])
            self._run_git(['branch', '-D', new_branch])
            raise e

def main():
    if len(sys.argv) < 2:
        print('Usage: gitmutate <repo_path> [mutation_count]')
        sys.exit(1)

    repo_path = sys.argv[1]
    mutation_count = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    try:
        mutator = GitMutator(repo_path)
        source_branch = mutator.current_branch()
        new_branch = mutator.mutate_branch(source_branch, mutation_count)
        print(f'Created mutated branch: {new_branch}')
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()