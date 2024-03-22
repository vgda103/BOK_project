# tokenizer class

import kss
from ekonlpy.tag import Mecab

class tokenizer_bok:

    def __init__(self) -> None:
        pass

    def sent_tokenizer(self):
        sents = kss.split_sentences(self)
        sents = [sent.replace('\n','') for sent in sents]
        return sents
    
    def word_tokenizer(self):
        tokenizer = Mecab()
        tokens = tokenizer.pos(self)
        return tokens
    
    def filter_tokens(self):
        filtered_tokens = []
        for token in self:
            if token[1] in ['NNG', 'VA', 'VAX','MAG','VA']:
                filtered_tokens.append(token)
        return filtered_tokens
    
    def txt2filtered(self):
        sents = kss.split_sentences(self)
        sents = [sent.replace('\n','') for sent in sents]
        all_filtered_tokens = []
        for sent in sents:
            tokenizer = Mecab()
            tokens = tokenizer.pos(sent)
            filtered_tokens = []
            for token in tokens:
                if token[1] in ['NNG', 'VA', 'VAX','MAG','VA']:
                    filtered_tokens.append(token)
            all_filtered_tokens.append(filtered_tokens)
        return all_filtered_tokens