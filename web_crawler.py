#Web crawler basics
#This web Crawler is just a simple version that has the basic components and logic

def get_page(url):
    if url in cache:
        return cache[url]
    return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

#Orders the results by ranking score from best to worst
def ordered_search(index, ranks, keyword):
    if keyword not in index:
        return None
    return quick_sort(index[keyword], ranks)

def quick_sort(pages, ranks):
    if len(pages) <= 1:
        return pages
    pivot_page = pages[0]
    left_part = []
    right_part = []
    for i in range(1, len(pages)):
        current_page_rank = ranks[pages[i]]
        if current_page_rank >= ranks[pivot_page]:
            left_part += [pages[i]]
        else:
            right_part += [pages[i]]
    sorted_left = sorted_right = []
    if left_part:
        sorted_left = quick_sort(left_part, ranks)
    if right_part:
        sorted_right = quick_sort(right_part, ranks)
    ordered_list = sorted_left + [pivot_page] + sorted_right
    return ordered_list
