
def dict_zip(*dicts):
    if not dicts:
        return

    n = len(dicts[0])
    if any(len(d) != n for d in dicts):
        raise ValueError('arguments must have the same length')

    for key, first_val in dicts[0].items():
        yield key, first_val, *(other[key] for other in dicts[1:])


def separate_dicts_example():
    names = {"UCaiL2GDNpLYH6Wokkk1VNcg": "mCoding",
             "UC7_gcs09iThXybpVgjHZ_7g": "PBS Space Time",
             "UCxHAlbZQNFU2LgEtiqd2Maw": "C++ Weekly With Jason Turner"}
    sub_counts = {"UCaiL2GDNpLYH6Wokkk1VNcg": 122_000,
                  "UC7_gcs09iThXybpVgjHZ_7g": 2_630_000,
                  "UCxHAlbZQNFU2LgEtiqd2Maw": 85_000}

    for cid in names:
        name = names[cid]
        sub_count = sub_counts[cid]
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')
    # prefer to loop over the items of the dict -> slightly more efficient
    # when you loop over items you do not have to compute the hash of the keys
    for cid, name in names.items():
        sub_count = sub_counts[cid]
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')
    # WRITEN BY US
    for cid, name, sub_count in dict_zip(names, sub_counts):
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def combined_dict_example():
    @dataclasses.dataclass
    class ChannelData:
        id: str
        name: str
        sub_count: int

    channels = [
        ChannelData(id="UCaiL2GDNpLYH6Wokkk1VNcg", name="mCoding", sub_count=122_000),
        ChannelData(id="UC7_gcs09iThXybpVgjHZ_7g", name="PBS Space Time", sub_count=2_630_000),
        ChannelData(id="UCxHAlbZQNFU2LgEtiqd2Maw", name="C++ Weekly With Jason Turner", sub_count=85_000),
    ]

    data = {channel.id: channel for channel in channels}

    for cid, channel in data.items():
        print(f'{channel.name} has {channel.sub_count} subscribers! Watch here: youtube.com/channel/{cid}')



def plain_zip_example():
    ids = ["UCaiL2GDNpLYH6Wokkk1VNcg", "UC7_gcs09iThXybpVgjHZ_7g", "UCxHAlbZQNFU2LgEtiqd2Maw"]
    names = ["mCoding", "PBS Space Time", "C++ Weekly With Jason Turner"]
    sub_counts = [122_000, 2_630_000, 85_000]
    # strict=True to ensure that all lists have the same length
    for cid, name, sub_count in zip(ids, names, sub_counts, strict=True):
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')
