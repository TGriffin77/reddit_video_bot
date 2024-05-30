

def verifyTitles(titleList):
    bad_words = [] # add a list of words to filter

    verifiedTitles = []
    for submission in titleList:
        submission[0] = submission[0].lower()
        if len(submission[0]) >= 121 or any(word in submission[0] for word in bad_words):
            continue
        else:
            verifiedTitles.append(submission)

    return verifiedTitles


def cleanTitles(titleList):
    censored_words = {} # dictionary: key = bad word, value = replace with this word

    cleanTitles = []
    for submission in titleList:
        for word in censored_words:
            if submission[0].__contains__(word):
                submission[0].replace(word, censored_words[word])

        cleanTitles.append(submission)
    return cleanTitles


def verifyComments(commentList):
    bad_words = [] # add a list of words to filter

    verifiedFinal = []
    verifiedComments = []
    for comment1d in commentList:
        verifiedComments = []
        for comment in comment1d:
            comment = comment.lower()
            if comment.__contains__('edit'):
                editIndex = comment.find('edit')
                temp = comment[editIndex + 4]
                if any(x == temp for x in ['-', ':', '\n']):
                    comment = comment[:editIndex]
            if (len(comment) < 70 or len(comment) > 600) or any(word in comment for word in bad_words):
                continue
            else:
                verifiedComments.append(comment)

        verifiedFinal.append(verifiedComments)
    return verifiedFinal


def cleanComments(commentList):
    censored_words = {} # dictionary: key = bad word, value = replace with this word


    finalComment = []
    for comment1D in commentList:
        cleanComments = []
        for comment in comment1D:
            newComment = comment.lower()
            for word in censored_words:
                if newComment.__contains__(word):
                    newComment = comment.replace(word, censored_words[word])
            cleanComments.append(newComment)
        finalComment.append(cleanComments)

    return finalComment