import torch
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
print(f'CUDA版本: {torch.version.cuda}')
if torch.cuda.is_available():
    print(f'GPU名称: {torch.cuda.get_device_name(0)}')
    cap = torch.cuda.get_device_capability(0)
    print(f'GPU计算能力: sm_{cap[0]}{cap[1]}')
    print(f'PyTorch支持的架构列表:')
    try:
        import torch.backends.cuda
        print(f'  (编译时架构信息需检查torch编译配置)')
    except:
        pass
else:
    print('GPU不可用')
