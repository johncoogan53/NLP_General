"""This will be a simple Markox text generator
which will use the function finish_sentence(sentence, n, corpus, randomize = False)
args:
    sentence[list]: list of tokens we are trying to build on
    n [int]: length of n-grams to use for prediction
    corpus: source corpus [list of tokens]
    randomize: stochastic or deterministic subsequent word selection"""
import numpy as np


def finish_sentence(sentence, n, corpus, randomize=False):
    """This function will take the input sentence, and use an n-gram model with stupid
    backoff (alpha =1) to assign subsequent words until a '.','?','!' or 10 total tokens
    """
    vocab = np.unique(np.array(corpus))
    final_sentence = np.array(sentence)
    vocabulary = vocab.tolist()

    best_word_indx = 0
    prob = 0
    # pylint: disable = Consider using enumerate instead of iterating with range and lenPylintC0200:consider-using-enumerate
    while (
        len(final_sentence) < 10
        and vocabulary[best_word_indx] != "."
        and vocabulary[best_word_indx] != "!"
        and vocabulary[best_word_indx] != "?"
    ):
        # sentence parse by n
        if n > len(final_sentence):
            prior = final_sentence
            pass
        else:
            prior = final_sentence[-(n - 1) :]
            pass

        best_word_indx = 0
        prob = 0
        for i in range(len(vocabulary)):
            # append vocabulary words onto prior and compute the backoff probability
            curr_gram = np.append(prior, vocabulary[i])
            curr_prob = compute_prob(curr_gram, corpus, n)
            if curr_prob > prob:  # handles the deterministic case
                prob = curr_prob
                best_word_indx = i
            elif curr_prob == prob and randomize is False:
                # draw from appropriate distribution?
                pass
            else:
                pass
        final_sentence = np.append(final_sentence, vocabulary[best_word_indx])
        print(final_sentence)
    return final_sentence


def compute_prob(n_gram, corpus, n):
    """Take the constructed n-gram from a vocab word and prior and compute backoff prob"""
    probability = 0
    if count(n_gram, corpus, n) > 0:
        probability = count(n_gram, corpus, n) / (len(corpus) - (n - 1))
        pass
    else:
        backoff = n_gram[1:]
        back_n = n - 1
        probability = compute_prob(backoff, corpus, back_n)
    return probability


def count(n_gram, corpus, n):
    """Compute the occurence of an n-gram in the corpus"""
    gram_count = 0
    for i in range(len(corpus) - (n - 1)):
        if np.array_equal(n_gram, corpus[i : i + n]):
            gram_count = gram_count + 1
    return gram_count


def main():
    corp = [
        "the",
        "cat",
        "is",
        "chubby",
        ",",
        "i",
        "want",
        "to",
        "pet",
        "his",
        "belly",
        ".",
    ]
    test_n = 3
    sent = ["the", "cat", "is"]
    print(finish_sentence(sent, test_n, corp))

    return None


if __name__ == "__main__":
    main()