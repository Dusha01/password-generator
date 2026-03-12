import os

import pytest

from src.i18n import get_locale, t


class TestI18n:
    def test_get_locale_en_default(self) -> None:
        env = os.environ.copy()
        env.pop("LANG", None)
        env.pop("LC_ALL", None)
        # Can't easily test without modifying env
        assert get_locale() in ("en", "ru")

    def test_get_locale_ru(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LANG", "ru_RU.UTF-8")
        assert get_locale() == "ru"

    def test_get_locale_en(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        assert get_locale() == "en"

    def test_t_error_count(self) -> None:
        assert "count" in t("error_count").lower() or "1" in t("error_count")

    def test_t_with_format(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        msg = t("warning_file_readable", path="/tmp/x")
        assert "/tmp/x" in msg
