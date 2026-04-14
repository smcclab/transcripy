import os
import shutil
import subprocess
import sys
import tempfile

from .helper import MultiFileHandler


class MultiVoiceExtractor(MultiFileHandler):
    def __init__(self, data_path: str, verbose: bool = False, model: str = 'htdemucs', vocals_only: bool = True) -> None:
        super().__init__(data_path, verbose, "raw_audio", "raw_audio_voices", "wav")
        self.vocals_only = vocals_only
        self.model = model

    def handler(self, input_file: str, output_file: str, file_idx: int) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [sys.executable, "-m", "demucs", "--name", self.model]
            if self.vocals_only:
                cmd += ["--two-stems=vocals"]
            cmd += ["-o", tmpdir, input_file]
            subprocess.run(
                cmd,
                check=True,
                capture_output=not self.verbose,
            )
            stem = os.path.splitext(os.path.basename(input_file))[0]
            vocals_path = os.path.join(tmpdir, self.model, stem, "vocals.wav")
            shutil.copy(vocals_path, output_file)
