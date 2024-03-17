from utils import *


async def main_checker():
    btc_denom = 100_000_000
    btc_round = 6
    btc_total = 0.0

    addresses = read_addresses()
    for index, address in enumerate(addresses):
        timeout = httpx.Timeout(60)

        async with httpx.AsyncClient(timeout=timeout) as client:
            if address.startswith('bc1p'):
                tasks = [
                    get_btc_balance(address=address, client=client),
                    get_magic_tokens(address=address),
                ]
                results = await asyncio.gather(*tasks)
                btc_balance, magic_tokens = results[0], results[1]

                btc_total += btc_balance.confirmed

                runestone = False
                for token in magic_tokens:
                    if token.collectionSymbol == 'runestone':
                        runestone = True
                        logger.success(f"#{index + 1} | {address} | "
                                       f"{btc_balance.confirmed / btc_denom:.{btc_round}f} $BTC | "
                                       f"runestone: https://magiceden.io/ordinals/item-details/{token.id}.")
                        break

                if not runestone:
                    logger.info(f"#{index + 1} | {address} | "
                                f"{btc_balance.confirmed / btc_denom:.{btc_round}f} $BTC.")
            else:
                tasks = [get_btc_balance(address=address, client=client)]
                results = await asyncio.gather(*tasks)
                btc_balance = results[0]

                btc_total += btc_balance.confirmed
                logger.info(f"#{index + 1} | {address} | not a taproot address | "
                            f"{btc_balance.confirmed / btc_denom:.{btc_round}f} $BTC.")

    logger.info('-' * 75)
    logger.info(f"{btc_total / btc_denom:.{btc_round}f} $BTC in total.")


if __name__ == '__main__':
    add_logger(version='v1.0')
    try:
        asyncio.run(main_checker())
    except Exception as e:
        logger.exception(e)
