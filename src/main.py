#!/usr/bin/env python3

import subprocess
import re
from typing import List, Tuple

class GitMutate:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = repo_path

    def get_diff(self, commit_range: str = 'HEAD~1..HEAD') -> str:
        """Get git diff for specified commit range"""
        cmd = ['git', '-C', self.repo_path, 'diff', commit_range]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def parse_diff(self, diff_text: str) -> List[Tuple[str, List[str], List[str]]]:
        """Parse git diff into list of (filename, removed_lines, added_lines)"""
        changes = []
        current_file = None
        removed_lines = []
        added_lines = []

        for line in diff_text.split('\n'):
            if line.startswith('diff --git'):
                if current_file:
                    changes.append((current_file, removed_lines, added_lines))
                    removed_lines = []
                    added_lines = []
                current_file = re.search(r'b/(.+)$', line).group(1)
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines.append(line[1:])
            elif line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:])

        if current_file:
            changes.append((current_file, removed_lines, added_lines))

        return changes

    def mutate_changes(self, changes: List[Tuple[str, List[str], List[str]]]) -> List[Tuple[str, List[str], List[str]]]:
        """Apply mutations to the changed lines"""
        mutated_changes = []

        for filename, removed, added in changes:
            mutated_added = []
            for line in added:
                # Example mutations:
                # 1. Add logging for function definitions
                if re.match(r'^\s*def\s+\w+\s*\(', line):
                    indent = len(line) - len(line.lstrip())
                    func_name = re.search(r'def\s+(\w+)', line).group(1)
                    mutated_added.append(line)
                    mutated_added.append(' ' * indent + f'print(f"Calling {func_name}")')
                else:
                    mutated_added.append(line)

            mutated_changes.append((filename, removed, mutated_added))

        return mutated_changes

    def apply_mutations(self, mutated_changes: List[Tuple[str, List[str], List[str]]]) -> None:
        """Apply mutated changes back to files"""
        for filename, _, added in mutated_changes:
            file_path = f"{self.repo_path}/{filename}"
            with open(file_path, 'r') as f:
                content = f.readlines()

            # Create new content with mutations
            new_content = []
            added_idx = 0
            for line in content:
                if added_idx < len(added) and line.strip() == added[added_idx].strip():
                    new_content.append(line)
                    added_idx += 1
                else:
                    new_content.append(line)

            # Write back to file
            with open(file_path, 'w') as f:
                f.writelines(new_content)

def main():
    mutator = GitMutate()
    diff = mutator.get_diff()
    changes = mutator.parse_diff(diff)
    mutated = mutator.mutate_changes(changes)
    mutator.apply_mutations(mutated)

if __name__ == '__main__':
    main()
