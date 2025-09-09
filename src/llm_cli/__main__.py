from __future__ import annotations
import argparse, sys

try:
    from llm_cli.commands.ask import AskCommand, AskCommandPayload
except Exception:
    import sys as _sys
    _sys.path.append("src")
    from llm_cli.commands.ask import AskCommand, AskCommandPayload

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="llm_cli",
        description="CLI de LLMs (OpenAI, Hugging Face) com padrões de projeto."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    ask = sub.add_parser("ask", help="Envia uma pergunta aos modelos.")
    ask.add_argument("prompt", type=str, help="Pergunta a ser enviada.")
    ask.add_argument("--providers", type=str, default="openai,openai-fake",
                     help="Lista separada por vírgulas. Ex.: openai,hf ou openai,openai-fake")
    ask.add_argument("--temperature", type=float, default=0.3)
    ask.add_argument("--strategy", type=str, default="keywords", choices=["keywords", "shortest"],
                     help="Critério de avaliação.")
    ask.add_argument("--keywords", type=str, default="",
                     help="Palavras-chave separadas por vírgula (para strategy=keywords).")

    return p

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)

    if args.cmd == "ask":
        providers = [p.strip() for p in args.providers.split(",") if p.strip()]
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
        payload = AskCommandPayload(
            prompt=args.prompt,
            providers=providers,
            temperature=args.temperature,
            strategy=args.strategy,
            keywords=keywords,
        )
        return AskCommand(payload).execute()

    return 1

if __name__ == "__main__":
    raise SystemExit(main())
