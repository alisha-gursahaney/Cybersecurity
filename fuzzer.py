# Name: Alisha Gursahaney
# Net Id: amg9zd

# Fuzzer skeleton code

import aiohttp, asyncio, args, json

async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    headers = {}
    for x in args.headers:
        hname, hvalue = x.split(": ")
        headers[hname] = hvalue
    #print(headers)

    # data = None
    # if args.data != None:
    #     data = json.loads(args.data)
    # print(data)

    # asynchronous loading of a URL:
    async with aiohttp.ClientSession() as session:
        with open(args.wordlist, 'r') as wordlist:
            # reading each line
            for line in wordlist:
                # reading each word
                for word in line.split():
                    new_string = args.url.replace("FUZZ", word)
                    async with session.request(method=args.method, url=new_string, headers=headers, data=args.data) as response:
                        await response.text()
                        if response.status in args.match_codes:
                            print(response.status, new_string)
                    for each in args.extensions:
                        new_url = args.url.replace("FUZZ", word+each)
                        async with session.request(method=args.method, url=new_url, headers=headers, data=args.data) as response:
                            await response.text()
                            if response.status in args.match_codes:
                                print(response.status, new_url)

# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    asyncio.run(fuzz(arguments))