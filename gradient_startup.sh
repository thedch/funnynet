git clone https://github.com/thedch/funnynet
cd funnynet
mkdir data
cd data
curl -O https://raw.githubusercontent.com/taivop/joke-dataset/master/reddit_jokes.json
curl -O https://raw.githubusercontent.com/taivop/joke-dataset/master/stupidstuff.json
cd ..
ln -s /notebooks/fastai/ fastai
python -m spacy download en
cd funnynet
mkdir ../courses/dl1/data/nietzsche
mkdir data/val
mkdir data/trn