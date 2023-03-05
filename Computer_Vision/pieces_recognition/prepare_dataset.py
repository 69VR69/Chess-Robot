from fileinput import filename
import os
import random
import shutil

splitSize = .85

# show the list of folders
dataDirList = os.listdir("C:\\Users\\ddbtn\\Downloads\\archive\\Chessman-image-dataset\\Chess")
print(dataDirList)


# lest vuild a function that will split the data between train and validation

def split_data(SOURCE, TRAINING, VALIDATION, SPLIT_SIZE):
    files = []

    for filename in os.listdir(SOURCE):
        file = SOURCE + filename
        print(file)
        if os.path.getsize(file) > 0:
            files.append(filename)
        else:
            print(filename + " - would ignore this file")

    print(len(files))

    trainLength = int(len(files) * SPLIT_SIZE)
    validLength = int(len(files) - trainLength)
    shuffledSet = random.sample(files, len(files))

    trainSet = shuffledSet[0:trainLength]
    validSet = shuffledSet[trainLength:]

    # copy the train images :
    for filename in trainSet:
        thisfile = SOURCE + filename
        destination = TRAINING + filename
        shutil.copyfile(thisfile, destination)

    # copy the validation images :
    for filename in validSet:
        thisfile = SOURCE + filename
        destination = VALIDATION + filename
        shutil.copyfile(thisfile, destination)


baseSourceDir = "C:\\Users\\ddbtn\\Downloads\\archive\\Chessman-image-dataset\\Chess"
trainSourceDir = "C:\\Users\\ddbtn\\PycharmProjects\\Chess-Robot\\Computer_Vision\\ressources\\dataset\\train"
validationSourceDir = "C:\\Users\\ddbtn\\PycharmProjects\\Chess-Robot\\Computer_Vision\\ressources\\dataset\\validation"

BishopSourceDir = baseSourceDir + "\\Bishop\\"
BishopTrainDir = trainSourceDir + "\\Bishop\\"
BishopValDir = validationSourceDir + "\\Bishop\\"

KingSourceDir = baseSourceDir + "\\King\\"
KingTrainDir = trainSourceDir + "\\King\\"
KingValDir = validationSourceDir + "\\King\\"

KnightSourceDir = baseSourceDir + "\\Knight\\"
KnightTrainDir = trainSourceDir + "\\Knight\\"
KnightValDir = validationSourceDir + "\\Knight\\"

PawnSourceDir = baseSourceDir + "\\Pawn\\"
PawnTrainDir = trainSourceDir + "\\Pawn\\"
PawnValDir = validationSourceDir + "\\Pawn\\"

QueenSourceDir = baseSourceDir + "\\Queen\\"
QueenTrainDir = trainSourceDir + "\\Queen\\"
QueenValDir = validationSourceDir + "\\Queen\\"

RookSourceDir = baseSourceDir + "\\Rook\\"
RookTrainDir = trainSourceDir + "\\Rook\\"
RookValDir = validationSourceDir + "\\Rook\\"

split_data(BishopSourceDir, BishopTrainDir, BishopValDir, splitSize)
split_data(KingSourceDir, KingTrainDir, KingValDir, splitSize)
split_data(KnightSourceDir, KnightTrainDir, KnightValDir, splitSize)
split_data(PawnSourceDir, PawnTrainDir, PawnValDir, splitSize)
split_data(QueenSourceDir, QueenTrainDir, QueenValDir, splitSize)
split_data(RookSourceDir, RookTrainDir, RookValDir, splitSize)
