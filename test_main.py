from typing import Any

from main import main


def test_main(capsys: Any) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from rag-backend!\n"
