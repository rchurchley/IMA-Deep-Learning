def generate_sku_and_url(filename, size=64):
    """From a flat text file containing SKUs, generate Target images."""

    with open(filename) as f:
        for line in f:
            sku = line.strip()
            url = 'http://scene7.targetimg1.com/is/image/Target/{}?wid={}'.format(sku, size)
            yield sku, url
