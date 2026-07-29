
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import load_and_preprocess_data, NewsDataset
from rnn_model import RNNTextClassifier


def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device), targets.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
        if batch_idx % 100 == 0:
            print(f'Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.4f}')
    
    return total_loss / len(train_loader), 100. * correct / total


def evaluate(model, test_loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    return total_loss / len(test_loader), 100. * correct / total


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    vocab_size = 20000
    embed_dim = 128
    hidden_dim = 256
    num_classes = 4
    num_layers = 2
    batch_size = 64
    epochs = 5
    learning_rate = 0.001
    max_len = 128
    
    train_texts, train_labels, test_texts, test_labels, vocab, tokenizer = load_and_preprocess_data()
    
    train_dataset = NewsDataset(train_texts, train_labels, vocab, tokenizer, max_len)
    test_dataset = NewsDataset(test_texts, test_labels, vocab, tokenizer, max_len)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    
    model = RNNTextClassifier(
        vocab_size=len(vocab),
        embed_dim=embed_dim,
        hidden_dim=hidden_dim,
        num_classes=num_classes,
        num_layers=num_layers,
        dropout=0.3
    ).to(device)
    
    print(f'Model architecture:\n{model}')
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    print('\nStarting training...')
    best_acc = 0
    train_losses = []
    train_accs = []
    test_losses = []
    test_accs = []
    
    for epoch in range(epochs):
        start_time = time.time()
        
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        test_loss, test_acc = evaluate(model, test_loader, criterion, device)
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        
        epoch_time = time.time() - start_time
        
        print(f'\nEpoch {epoch+1}/{epochs}')
        print(f'Train Loss: {train_loss:.4f}, Train Accuracy: {train_acc:.2f}%')
        print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.2f}%')
        print(f'Time: {epoch_time:.2f}s')
        
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), 'models/rnn_best_model.pth')
            print(f'Model saved with Test Accuracy: {best_acc:.2f}%')
    
    print(f'\nTraining completed! Best Test Accuracy: {best_acc:.2f}%')
    
    print('\nTesting best model...')
    model.load_state_dict(torch.load('models/rnn_best_model.pth'))
    final_loss, final_acc = evaluate(model, test_loader, criterion, device)
    print(f'Final Test Loss: {final_loss:.4f}, Final Test Accuracy: {final_acc:.2f}%')
    
    results_file = 'results/training_results.txt'
    with open(results_file, 'w') as f:
        f.write('NLP News Classification - RNN Model Results\n')
        f.write('='*50 + '\n\n')
        f.write(f'Vocab Size: {len(vocab)}\n')
        f.write(f'Embed Dim: {embed_dim}\n')
        f.write(f'Hidden Dim: {hidden_dim}\n')
        f.write(f'Num Layers: {num_layers}\n')
        f.write(f'Batch Size: {batch_size}\n')
        f.write(f'Epochs: {epochs}\n')
        f.write(f'Learning Rate: {learning_rate}\n\n')
        f.write(f'Best Test Accuracy: {best_acc:.2f}%\n')
        f.write(f'Final Test Accuracy: {final_acc:.2f}%\n\n')
        f.write('Training History:\n')
        f.write('-'*50 + '\n')
        for i in range(epochs):
            f.write(f'Epoch {i+1} - Train Loss: {train_losses[i]:.4f}, Train Acc: {train_accs[i]:.2f}%, Test Loss: {test_losses[i]:.4f}, Test Acc: {test_accs[i]:.2f}%\n')
    
    print(f'\nResults saved to {results_file}')


if __name__ == '__main__':
    main()
