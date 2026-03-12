import pytest

from src.modules.generator.passphrase import generate_passphrase


class TestGeneratePassphrase:
    def test_default_four_words(self) -> None:
        pw = generate_passphrase()
        words = pw.split("-")
        assert len(words) == 4

    def test_custom_word_count(self) -> None:
        pw = generate_passphrase(words_count=6)
        words = pw.split("-")
        assert len(words) == 6

    def test_custom_separator(self) -> None:
        pw = generate_passphrase(words_count=3, separator="_")
        words = pw.split("_")
        assert len(words) == 3

    def test_different_each_call(self) -> None:
        results = {generate_passphrase() for _ in range(50)}
        assert len(results) == 50

    def test_words_from_list(self) -> None:
        from src.modules.generator.wordlist import WORDS

        pw = generate_passphrase(words_count=10)
        words = pw.split("-")
        assert all(w in WORDS for w in words)

    def test_zero_words_raises(self) -> None:
        with pytest.raises(ValueError, match="at least 1"):
            generate_passphrase(words_count=0)

    def test_too_many_words_raises(self) -> None:
        with pytest.raises(ValueError, match="must not exceed 20"):
            generate_passphrase(words_count=21)
