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
                #sent_L.append('\n')
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
    parser.add_argument('--indir', type=str, required=True)
    parser.add_argument('--outdir', type=str, required=True)
    parser.add_argument('--num_doc',type=int,default=4783)
    args = parser.parse_args()
    

    file_list = list(sorted(glob(os.path.join(args.indir, '*.txt'))))

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    
    f = open(os.path.join(args.outdir,str(1)+'.txt'),'w')
    for i, file_path in enumerate(file_list):
        if i%300 == 0:
            if i>0:
              f.close()
              f = open(os.path.join(args.outdir,str(int(i/300)+1)+'.txt'),'w')
        sents, n_sent = convert_into_sentences(open(file_path).readlines())
        sent_collection = '\n'.join(sents)
        sent_collection = sent_collection + '\n\n\n\n'
        f.write(sent_collection)
        if i > args.num_doc:
            break

        #print('\n'.join(sents))
        #print('\n\n\n\n')
        sys.stderr.write(
            '{}/{}\t{}\t{}\n'.format(i, len(file_list), n_sent, file_path))
