def main():
    from sync import sync
    from parse import parse

    syncing = False
    parsing = True
    if syncing:
        sync()
    if parsing:
        parse()



if __name__ == "__main__":
    main()