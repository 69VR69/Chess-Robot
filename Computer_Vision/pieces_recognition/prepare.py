import os

# show the list of folders
dataDirList = os.listdir("C:\\Users\\ddbtn\\Downloads\\archive\\Chessman-image-dataset\\Chess")
print(dataDirList)

# lets create our working images folder
# this will only run once

baseDir = "C:\\Users\\ddbtn\\PycharmProjects\\Chess-Robot\\Computer_Vision\\ressources\\dataset"

# train folders

trainData = os.path.join(baseDir, 'train2')
os.mkdir(trainData)

validationData = os.path.join(baseDir, 'validation2')
os.mkdir(validationData)

trainBishopData = os.path.join(trainData, 'bishop_b')
os.mkdir(trainBishopData)
trainKingData = os.path.join(trainData, 'King')
os.mkdir(trainKingData)
trainKnightData = os.path.join(trainData, 'Knight')
os.mkdir(trainKnightData)
trainPawnData = os.path.join(trainData, 'Pawn')
os.mkdir(trainPawnData)
trainQueenData = os.path.join(trainData, 'Queen')
os.mkdir(trainQueenData)
trainRookData = os.path.join(trainData, 'Rook')
os.mkdir(trainRookData)

# validation folders
valBishopData = os.path.join(validationData, 'Bishop')
os.mkdir(valBishopData)
valKingData = os.path.join(validationData, 'King')
os.mkdir(valKingData)
valKnightData = os.path.join(validationData, 'Knight')
os.mkdir(valKnightData)
valPawnData = os.path.join(validationData, 'Pawn')
os.mkdir(valPawnData)
valQueenData = os.path.join(validationData, 'Queen')
os.mkdir(valQueenData)
valRookData = os.path.join(validationData, 'Rook')
os.mkdir(valRookData)
