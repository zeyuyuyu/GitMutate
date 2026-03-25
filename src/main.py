#!/usr/bin/env python3

import git
import random
import sys
from pathlib import Path
from typing import List, Optional

class GitMutator:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.base_branch = self.repo.active_branch

    def create_mutation_branch(self, name: str) -> git.Head:
        """Create a new branch for mutations"""
        new_branch = self.repo.create_head(f'mutation/{name}')
        new_branch.checkout()
        return new_branch

    def smart_resolve_conflicts(self, file_path: str) -> bool:
        """Intelligently resolve merge conflicts in a file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            if '<<<<<<< HEAD' not in content:
                return True

            resolved = []
            in_conflict = False
            current_chunk = []
            incoming_chunk = []

            for line in content.split('\
'):
                if line.startswith('<<<<<<< HEAD'):
                    in_conflict = True
                    continue
                elif line.startswith('======='):
                    current_chunk = []
                    continue
                elif line.startswith('>>>>>>>'):
                    # Randomly select one version or merge both
                    if random.random() < 0.5:
                        resolved.extend(current_chunk or incoming_chunk)
                    else:
                        resolved.extend(current_chunk + incoming_chunk)
                    current_chunk = []
                    incoming_chunk = []
                    in_conflict = False
                    continue

                if in_conflict:
                    current_chunk.append(line)
                else:
                    resolved.append(line)

            with open(file_path, 'w') as f:
                f.write('\
'.join(resolved))

            self.repo.index.add([file_path])
            return True

        except Exception as e:
            print(f'Error resolving conflicts: {str(e)}')
            return False

    def apply_mutations(self, files: List[str], mutation_rate: float = 0.1) -> bool:
        """Apply random mutations to specified files"""
        try:
            for file_path in files:
                if not Path(file_path).exists():
                    continue

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                mutated = False
                for i in range(len(lines)):
                    if random.random() < mutation_rate:
                        mutation_type = random.choice(['modify', 'duplicate', 'delete'])
                        
                        if mutation_type == 'modify':
                            lines[i] = lines[i].strip() + ' # Mutated\
'
                        elif mutation_type == 'duplicate':
                            lines.insert(i, lines[i])
                        elif mutation_type == 'delete':
                            lines[i] = ''
                        
                        mutated = True

                if mutated:
                    with open(file_path, 'w') as f:
                        f.writelines(lines)
                    self.repo.index.add([file_path])

            if self.repo.is_dirty():
                self.repo.index.commit('feat: applied mutations')
                return True

            return False

        except Exception as e:
            print(f'Error applying mutations: {str(e)}')
            return False

    def merge_mutations(self, target_branch: str) -> bool:
        """Merge mutations back to target branch with conflict resolution"""
        try:
            target = self.repo.heads[target_branch]
            target.checkout()

            try:
                self.repo.git.merge('--no-ff', str(self.repo.active_branch))
                return True
            except git.GitCommandError:
                # Handle merge conflicts
                unmerged_blobs = self.repo.index.unmerged_blobs()
                for file_path in unmerged_blobs:
                    if not self.smart_resolve_conflicts(file_path):
                        self.repo.git.execute(['git', 'merge', '--abort'])
                        return False

                self.repo.index.commit('feat: merged mutations with resolved conflicts')
                return True

        except Exception as e:
            print(f'Error merging mutations: {str(e)}')
            return False

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py <repo_path> [files...]')
        sys.exit(1)

    repo_path = sys.argv[1]
    files = sys.argv[2:] if len(sys.argv) > 2 else ['.']

    mutator = GitMutator(repo_path)
    branch_name = f'mutation_{random.randint(1000, 9999)}'
    
    mutator.create_mutation_branch(branch_name)
    if mutator.apply_mutations(files):
        if mutator.merge_mutations('master'):
            print('Successfully applied and merged mutations')
        else:
            print('Failed to merge mutations')
    else:
        print('No mutations were applied')

if __name__ == '__main__':
    main()
