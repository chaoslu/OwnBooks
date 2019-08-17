import os
import sys
import argparse
from glob import glob

from blingfire import text_to_sentences

#file_dir = sys.argv[1]
file_dir = 'out_txts'


def convert_into_sentences(lines):
    stack = []
    sent_L = []
    n_sent = 0
    for chunk in lines:
        if not chunk.strip():
            if stack:
                sents = text_to_sentences(
                    " ".join(stack).strip().replace('\n', ' ')).split('\n')
                sent_L.extend(sents)
                n_sent += len(sents)
                sent_L.append('\n')
                stack = []
            continue
        stack.append(chunk.strip())

    if stack:
        sents = text_to_sentences(
            " ".join(stack).strip().replace('\n', ' ')).split('\n')
        sent_L.extend(sents)
        n_sent += len(sents)
    return sent_L, n_sent

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--in-dir', '--in', type=str, required=True)
    parser.add_argument('--out-dir', '--out', type=str, required=True)
    args = parser.parse_args()


    file_list = list(sorted(glob(os.path.join(args.in_dir, '*.txt'))))

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    for i, file_path in enumerate(file_list):
        sents, n_sent = convert_into_sentences(open(file_path).readlines())
        sent_collection = '\n'.join(sents)
        sent_collection = sent_collection + '\n\n\n\n'
        if i>=300 & i%300 == 0:
            with open(args.out_dir+str(int(i/300))+'.txt','w') as f:
                f.write(sent_collection)

        #print('\n'.join(sents))
        #print('\n\n\n\n')
        sys.stderr.write(
            '{}/{}\t{}\t{}\n'.format(i, len(file_list), n_sent, file_path))
