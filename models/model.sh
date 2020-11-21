#! /bin/bash

python labels.py --model 'TCN' --slice_length 64 --input_size 5 --normalization NO
python labels.py --model 'TCN' --slice_length 64 --input_size 4 --normalization NO
python labels.py --model 'TCN' --slice_length 64 --input_size 5 --normalization Yes

python labels.py --model 'LSTM' --slice_length 64 --input_size 5 --normalization NO
python labels.py --model 'LSTM' --slice_length 64 --input_size 4 --normalization NO
python labels.py --model 'LSTM' --slice_length 64 --input_size 5 --normalization Yes

python labels.py --model 'GRU' --slice_length 64 --input_size 5 --normalization NO
python labels.py --model 'GRU' --slice_length 64 --input_size 4 --normalization NO
python labels.py --model 'GRU' --slice_length 64 --input_size 5 --normalization Yes

python labels.py --model 'TCN' --slice_length 320 --input_size 5 --normalization NO
python labels.py --model 'TCN' --slice_length 320 --input_size 4 --normalization NO
python labels.py --model 'TCN' --slice_length 320 --input_size 5 --normalization Yes

python labels.py --model 'LSTM' --slice_length 320 --input_size 5 --normalization NO
python labels.py --model 'LSTM' --slice_length 320 --input_size 4 --normalization NO
python labels.py --model 'LSTM' --slice_length 320 --input_size 5 --normalization Yes

python labels.py --model 'GRU' --slice_length 320 --input_size 5 --normalization NO
python labels.py --model 'GRU' --slice_length 320 --input_size 4 --normalization NO
python labels.py --model 'GRU' --slice_length 320 --input_size 5 --normalization Yes

