require 'nn'
require 'paths'
if (not paths.filep("cifar10torchsmall.zip")) then
    os.execute('wget -c https://s3.amazonaws.com/torch7/data/cifar10torchsmall.zip')
    os.execute('unzip cifar10torchsmall.zip')
end
trainset = torch.load('cifar10-train.t7')
testset = torch.load('cifar10-test.t7')
classes = {'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'}
setmetatable(trainset, 
{__index = function(t, i)
    return {t.data[i], t.label[i]}
end}
);
trainset.data = trainset.data:double() --将数据转化为DoubleTensor

function trainset:size()
    return self.data:size(1)
end
mean = {} --存储均值，正则化测试数据特征
stdv = {} --存储标准差
for i=1,3 do
    mean[i] = trainset.data[{{}, {i}, {}, {}}]:mean()
    print('Channel ' .. i .. ', Mean: ' .. mean[i])
    trainset.data[{ {}, {i}, {}, {} }]:add(-mean[i]) -- mean subtraction

    stdv[i] = trainset.data[{ {}, {i}, {}, {} }]:std()
    print('Channel ' .. i .. ', Standard Deviation: ' .. stdv[i])
    trainset.data[{ {}, {i}, {}, {} }]:div(stdv[i]) -- std scaling
end

net = nn.Sequential()
net:add(nn.SpatialConvolution(3, 6, 5, 5)) -- 3 input image channels, 6 output channels, 5*5 convolution kernel
net:add(nn.ReLU()) --non-linearity
net:add(nn.SpatialMaxPooling(2,2,2,2)) -- A max-pooling operation that looks at 2*2 windows and finds the max
net:add(nn.SpatialConvolution(6, 16, 5, 5))
net:add(nn.ReLU())
net:add(nn.SpatialMaxPooling(2,2,2,2))
net:add(nn.View(16*5*5)) --reshape from a 3D tensor of 16*5*5 into 1D tensor of 16*5*5
net:add(nn.Linear(16*5*5, 120)) --fully connected layer (matrix multiplication between input and weight)
net:add(nn.ReLU()) --non-linearity
net:add(nn.Linear(120, 84))
net:add(nn.ReLU())
net:add(nn.Linear(84, 10)) --10 is the number of output of the network (in this case, 10 digits)
net:add(nn.LogSoftMax()) --converts the output to a log-probability Useful for classification problems
criterion = nn.ClassNLLCriterion()
trainer = nn.StochasticGradient(net, criterion)
trainer.learningRate = 0.001
trainer.maxIteration = 5
trainer:train(trainset)
testset.data = testset.data:double()
for i=1,3 do --over each image channel
    testset.data[{ {}, {i}, {}, {} }]:add(-mean[i])
    testset.data[{ {}, {i}, {}, {} }]:div(stdv[i])
end
predicted = net:forward(testset.data[100])
print(classes[testset.label[100]])
print(predicted:exp())
for i=1,predicted:size(1) do
    print(classes[i], predicted[i])
end

correct = 0
for i=1,10000 do
    local groundtruth = testset.label[i]
    local prediction = net:forward(testset.data[i])
    local confidences, indices = torch.sort(prediction, true)
    if groundtruth == indices[1] then
        correct = correct + 1
    end
end
print(correct, 100*correct/10000 .. ' % ')
class_performance = {0,0,0,0,0,0,0,0,0,0}
for i=1,10000 do
    local groundtruth = testset.label[i]
    local prediction = net:forward(testset.data[i])
    local confidences, indices = torch.sort(prediction, true)
    if groundtruth == indices[1] then
        class_performance[groundtruth] = class_performance[groundtruth] + 1
    end
end

for i=1,#classes do
    print(classes[i], 100*class_performance[i]/1000 .. ' %')
end

--两个卷积层，两个池化层，一个全链接 一个softmax层
