from utils.logger import setup_logger
from utils.parser import parse_args

def main():
    logger = setup_logger()
    args, remaining = parse_args()
    logger.info("Starting CorteXForge...")
    logger.info(f"Radio role={args.role}")

    if args.role == "rx":
        from radio.rx import main as rx_main
        rx_main()
    elif args.role == "tx":
        from radio.tx import main as tx_main
        tx_main()
    else:
        raise ValueError(f"Unknown role: {args.role}")


if __name__ == "__main__":
    main()
