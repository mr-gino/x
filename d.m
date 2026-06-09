% Dawid Skocz (127770)
% Kolokwium 2 - Sieci neuronowe

clear all;
close all;
clc;

% a) Wczytanie danych

data = readtable('drug200.csv');

disp('Dane wczytane');

% b) Usunięcie brakujących danych

data = rmmissing(data);

disp('Usunięto brakujące dane');

% c) Kodowanie danych nienumerycznych

for i=1:width(data)

    if iscell(data{:,i}) || isstring(data{:,i}) || ...
            iscategorical(data{:,i})

        data.(i) = grp2idx(categorical(data{:,i}));

    end

end

disp('Zakodowano dane nienumeryczne');

% d) Normalizacja

X = table2array(data(:,1:end-1));

X = normalize(X);

Y = data.Drug; % Wyjścia oczekiwane

sko = X';
daw = dummyvar(categorical(Y))';

N = size(sko,2);

rng('default');

idx = randperm(N);

trainSize = round(0.90*N);

trainIdx = idx(1:trainSize);
testIdx = idx(trainSize+1:end);

sko_train = sko(:,trainIdx);
daw_train = daw(:,trainIdx);

sko_test = sko(:,testIdx);
daw_test = daw(:,testIdx);

% e) Projekt sieci neuronowej

hiddenLayerSize = 10;

net = patternnet(hiddenLayerSize);

net.layers{1}.transferFcn = 'tansig';
net.layers{2}.transferFcn = 'softmax';

net.trainFcn = 'trainlm';

net.performFcn = 'mse';

% f) Uczenie sieci

net = train(net,sko_train,daw_train);

% Testowanie

wynik = net(sko_test);

[~,pred] = max(wynik);
[~,real] = max(daw_test);

% g) Ocena jakości

cm = confusionmat(real,pred);

disp('Macierz pomylek');
disp(cm);

accuracy = sum(pred==real)/length(real);

fprintf('Accuracy = %.4f\n',accuracy);

% Precision i Recall

classes = unique(real);

for i=1:length(classes)

    TP = cm(i,i);

    FP = sum(cm(:,i)) - TP;

    FN = sum(cm(i,:)) - TP;

    precision = TP/(TP+FP);

    recall = TP/(TP+FN);

    fprintf('\nKlasa %d\n',i);
    fprintf('Precision = %.4f\n',precision);
    fprintf('Recall = %.4f\n',recall);

end


% Wnioski
%
% Liczba neuronow ukrytych: 10
%
% Funkcja aktywacji:
% tansig (warstwa ukryta)
% softmax (warstwa wyjsciowa)
%
% Funkcja celu:
% mse
%
% Algorytm uczenia:
% trainlm
%
% Accuracy:
%
% Najlepiej rozpoznawana klasa:
%
% Najgorzej rozpoznawana klasa:
%
% Najbardziej wiarygodna klasyfikacja:
%