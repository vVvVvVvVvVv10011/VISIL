import subprocess
from visil.sigil_state import SigilStateExtractor


class SigilGitBinder:

    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.extractor = SigilStateExtractor(repo_path)

    # -------------------------
    # PROCESS EVENT → COMMIT
    # -------------------------
    def process_event(self, event, graph):

        message = self.extractor.build_commit_message(
            graph,
            base_msg=event.get("message", "VISIL commit")
        )

        self._git_add_all()
        self._git_commit(message)

        return message

    # -------------------------
    # STAGE ALL CHANGES
    # -------------------------
    def _git_add_all(self):
        subprocess.run(["git", "add", "."], cwd=self.repo_path)

    # -------------------------
    # COMMIT
    # -------------------------
    def _git_commit(self, message):
        subprocess.run(["git", "commit", "-m", message], cwd=self.repo_path)
