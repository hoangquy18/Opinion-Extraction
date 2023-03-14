import re   
import numpy as np
class Preprocessing:
    def __init__(self):
        self.vowels_to_ids = {}
        self.vowels_table = [
            ['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a' ],
            ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
            ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
            ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e' ],
            ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
            ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i' ],
            ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o' ],
            ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'o'],
            ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
            ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u' ],
            ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
            ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y' ]
        ]
        pass

    def createVowelsTable(self):
        """Create Vowels Table"""
        for i in range(len(self.vowels_table)):
            for j in range(len(self.vowels_table[i]) - 1):
                self.vowels_to_ids[self.vowels_table[i][j]] = (i, j)

    def IsValidVietnameseWord(self,word):
        """Nguyên âm chỉ có thể đứng chung với nguyên âm. Một từ không thể có 2 nguyên âm cách nhau bởi 1 phụ âm"""
        chars = list(word)
        #nguyen am
        vowel_index = -1
        for i in range(len(chars)):
            idx_vowel_table = self.vowels_to_ids.get(chars[i],(-1,-1))[0]
            if idx_vowel_table != -1:
                if vowel_index == -1:
                    vowel_index = i 
                else:
                    if i - vowel_index != 1:
                        return False
                    vowel_index = i
        return True

    def WordStandardized(self,word):
        """Standardize Word"""
        if not self.IsValidVietnameseWord(word):
            return word

        chars = list(word)
        vowel_indexes = []

        # tìm vị trí nguyên âm
        qu_or_gi = False
        thanh_dieu = 0
        for i in range(len(chars)):
            vowel_table_row, vowel_table_col = self.vowels_to_ids.get(chars[i],(-1,-1))
            if vowel_table_row == -1 :
                continue
            # qu
            if vowel_table_row == 9:
                if i != 0 and chars[i-1] == 'q':
                    chars[i] = 'u'
                    qu_or_gi = True
            # gi
            elif vowel_table_row == 5:
                if i != 0 and chars[i-1] == 'g':
                    chars[i] = 'i'
                    qu_or_gi = True

            # có chứa thanh điệu
            if vowel_table_col != 0:
                thanh_dieu = vowel_table_col
                chars[i] = self.vowels_table[vowel_table_row][0]

            vowel_indexes.append(i)
        # 1 nguyên âm
        if len(vowel_indexes) == 1:
            c = chars[vowel_indexes[0]]
            chars[vowel_indexes[0]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
            return ''.join(chars)

        for idx_vowel in vowel_indexes:
            vowel_table_row, vowel_table_col = self.vowels_to_ids.get(chars[idx_vowel],(-1,-1))
            #ê, ơ, ô
            if vowel_table_row == 4 or vowel_table_row == 7 or vowel_table_row == 8:
                c = chars[idx_vowel]
                chars[idx_vowel] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                return ''.join(chars)

            # kiểm tra qu và gi, 2-3 nguyên âm thì nguyên âm thứ 2 chứa dấu
            if qu_or_gi:
                if len(vowel_indexes) == 2 or len(vowel_indexes) == 3:
                    c = chars[vowel_indexes[1]]
                    chars[vowel_indexes[1]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                return ''.join(chars)
            
            # 2 nguyên âm
            if len(vowel_indexes) == 2:
                # âm cuối là nguyên âm
                if vowel_indexes[-1] == len(chars) - 1:
                    c = chars[vowel_indexes[0]]
                    chars[vowel_indexes[0]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                else:
                    c = chars[vowel_indexes[-1]]
                    chars[vowel_indexes[-1]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                return ''.join(chars)
            
            elif len(vowel_indexes) == 3:
                # âm cuối là nguyên âm
                if vowel_indexes[-1] == len(chars) - 1:
                    c = chars[vowel_indexes[1]]
                    chars[vowel_indexes[1]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                else:
                    c = chars[vowel_indexes[-1]]
                    chars[vowel_indexes[-1]] = self.vowels_table[self.vowels_to_ids[c][0]][thanh_dieu]
                return ''.join(chars)

        return ''.join(chars)

    def TextNormalized(self,text):

        #Chuyen sang viet thuong
        text = text.lower()
        # Rút gọn từ kéo dài
        text = re.sub(r'(\w)\1+',r'\1',text)

        # xóa các emoji dư thừa
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'',text) # no emoji
            
        # dấu sát từ thì cách ra
        text = re.sub(r'([\.\?\/\\\-\+~`#$%!:\"\;\'\|\{\}\[\],])', r' \1 ',text)
        text = text.replace(".",',')
        text = text.split()
        # chuẩn hóa thanh điệu
        for i in range(len(text)):
            text[i] = self.WordStandardized(text[i])

        text = ' '.join(text)

        # text = word_tokenize(text,format = 'text')

        # xóa kí tự thừa 
        # text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÍÌỈĨỊÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ_]', ' ', text)
        text = text.strip('\"').strip()

        # xóa space
        text = re.sub(r"( )\1+",r'\1',text)
        
        return text
def word_tag_idx():
    f= open('word2vec_vi_syllables_100dims.txt','r',encoding='utf-8')
    words = []
    embedding_words = {}

    i = 0
    for line in f:
        if i == 0:
            i+= 1
            continue
        value = line.split(' ')
        word = value[0]
        words.append(word)
        try:
            coefs = value[1:]
            embedding_words[word] = np.asarray(coefs,dtype=np.float32)
        except:
            pass
    embedding_dim = 100
    num_word = len(words)
    word2idx = {w:i for i,w in enumerate(words,start = 2)}
    word2idx['PAD'] = 0
    word2idx['UNK'] = 1    
       
    idx2word = {i:w for w,i in word2idx.items()}

    tags = ['B-GENERAL#POSITIVE', 'B-GENERAL#NEUTRAL', 'B-GENERAL#NEGATIVE',
       'B-DISPLAY#POSITIVE', 'B-DISPLAY#NEUTRAL', 'B-DISPLAY#NEGATIVE',
       'B-BATTERY#POSITIVE', 'B-BATTERY#NEUTRAL', 'B-BATTERY#NEGATIVE',
       'B-TOUCHPAD#POSITIVE', 'B-TOUCHPAD#NEUTRAL', 'B-TOUCHPAD#NEGATIVE',
       'B-KEYBOARD#POSITIVE', 'B-KEYBOARD#NEUTRAL', 'B-KEYBOARD#NEGATIVE',
       'B-SERVICE#POSITIVE', 'B-SERVICE#NEUTRAL', 'B-SERVICE#NEGATIVE',
       'B-WARRATY#POSITIVE', 'B-WARRATY#NEUTRAL', 'B-WARRATY#NEGATIVE',
       'B-STORAGE#POSITIVE', 'B-STORAGE#NEUTRAL', 'B-STORAGE#NEGATIVE',
       'B-CONNECTIVITY#POSITIVE', 'B-CONNECTIVITY#NEUTRAL',
       'B-CONNECTIVITY#NEGATIVE', 'B-MULTIMEDIA_DEVICES#POSITIVE',
       'B-MULTIMEDIA_DEVICES#NEUTRAL', 'B-MULTIMEDIA_DEVICES#NEGATIVE',
       'B-DESIGN#POSITIVE', 'B-DESIGN#NEUTRAL', 'B-DESIGN#NEGATIVE',
       'B-FANS_COOLING#POSITIVE', 'B-FANS_COOLING#NEUTRAL',
       'B-FANS_COOLING#NEGATIVE', 'B-PERFORMANCE#POSITIVE',
       'B-PERFORMANCE#NEUTRAL', 'B-PERFORMANCE#NEGATIVE',
       'B-PRICE#POSITIVE', 'B-PRICE#NEUTRAL', 'B-PRICE#NEGATIVE',
       'B-FEATURES#POSITIVE', 'B-FEATURES#NEUTRAL', 'B-FEATURES#NEGATIVE',
       'I-GENERAL#POSITIVE', 'I-GENERAL#NEUTRAL', 'I-GENERAL#NEGATIVE',
       'I-DISPLAY#POSITIVE', 'I-DISPLAY#NEUTRAL', 'I-DISPLAY#NEGATIVE',
       'I-BATTERY#POSITIVE', 'I-BATTERY#NEUTRAL', 'I-BATTERY#NEGATIVE',
       'I-TOUCHPAD#POSITIVE', 'I-TOUCHPAD#NEUTRAL', 'I-TOUCHPAD#NEGATIVE',
       'I-KEYBOARD#POSITIVE', 'I-KEYBOARD#NEUTRAL', 'I-KEYBOARD#NEGATIVE',
       'I-SERVICE#POSITIVE', 'I-SERVICE#NEUTRAL', 'I-SERVICE#NEGATIVE',
       'I-WARRATY#POSITIVE', 'I-WARRATY#NEUTRAL', 'I-WARRATY#NEGATIVE',
       'I-STORAGE#POSITIVE', 'I-STORAGE#NEUTRAL', 'I-STORAGE#NEGATIVE',
       'I-CONNECTIVITY#POSITIVE', 'I-CONNECTIVITY#NEUTRAL',
       'I-CONNECTIVITY#NEGATIVE', 'I-MULTIMEDIA_DEVICES#POSITIVE',
       'I-MULTIMEDIA_DEVICES#NEUTRAL', 'I-MULTIMEDIA_DEVICES#NEGATIVE',
       'I-DESIGN#POSITIVE', 'I-DESIGN#NEUTRAL', 'I-DESIGN#NEGATIVE',
       'I-FANS_COOLING#POSITIVE', 'I-FANS_COOLING#NEUTRAL',
       'I-FANS_COOLING#NEGATIVE', 'I-PERFORMANCE#POSITIVE',
       'I-PERFORMANCE#NEUTRAL', 'I-PERFORMANCE#NEGATIVE',
       'I-PRICE#POSITIVE', 'I-PRICE#NEUTRAL', 'I-PRICE#NEGATIVE',
       'I-FEATURES#POSITIVE', 'I-FEATURES#NEUTRAL', 'I-FEATURES#NEGATIVE',
       'O']
    tag2idx = {t:i+1 for i,t in enumerate(tags)}
    tag2idx["PAD"] = 0
    idx2tag = {i:t for t,i in tag2idx.items()}

    embedding_matrix = np.ones((num_word,embedding_dim))
    for w,i in word2idx.items():
        if i > 10000:
            continue
        embedding_vector = embedding_words.get(w)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
        else:
            embedding_matrix[i] = np.random.randn(100)
    
    return word2idx,idx2word,tag2idx,idx2tag
