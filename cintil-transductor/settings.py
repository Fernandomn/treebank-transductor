def init():
    global posDict
    global conjTag
    global conjBarTag
    global conjPTag
    global conjList
    global conjList2
    global pointTag
    global pointList
    global removeTag
    global CTag
    global CPTag
    global CPBarTag
    global CWordDict
    global clitList
    global isFirstQuoteMark
    global tagOcc
    global wordLevelTags
    global splitTag
    global tagsProblematicas

    CWordDict = {}
    pointList = ['"', "'", "...", "-", "/", "-lrb-", "-rrb-", ",", ".", "*"]
    conjTag = 'CC'
    conjBarTag = '_CONJP_'
    conjPTag = 'CONJP'
    CTag = 'CC'
    CPBarTag = '_CP_'
    CPTag = 'CONJP'
    pointTag = 'PNT'
    removeTag = '_TOREMOVE_'
    posDict = {}
    conjList = []
    conjList2 = []
    clitList = []
    tagOcc = {}
    tagsProblematicas = [conjBarTag, CPBarTag]
    wordLevelTags = [conjPTag, CPTag, conjBarTag]
    splitTag = '_SPLIT_'
