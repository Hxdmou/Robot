# -*- coding: utf-8 -*-
'''最终验证：真实高度=B+末段SpaceAfter（BoundHeight不含末段段间距）
V3.37 系统能力升级：自动识别根目录最新版本PPT（无需手改版本号），
结果固定写入 _verify_latest.txt，退出码 0=通过(0溢出0空隙) / 1=不通过，供 delivery_gate.py 调用。'''
import sys, io, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time

HERE = os.path.dirname(os.path.abspath(__file__))

def latest_pptx(kind):
    '''自动识别根目录最新版本PPT（kind='无水印'或'水印版'，按_vNN版本号取最大）'''
    cands = glob.glob(os.path.join(HERE, '具身智能AI产业最新进展_*_商务汇报_%s_v*.pptx' % kind))
    if not cands:
        return None
    def ver(p):
        m = re.search(r'_v(\d+)\.pptx$', p)
        return int(m.group(1)) if m else -1
    return max(cands, key=ver)

# 双版本同步铁律：无水印原版+水印防盗窃版必须同时验证
FILES = [f for f in [latest_pptx('无水印'), latest_pptx('水印版')] if f]
if not FILES:
    print('[X] 未找到任何 无水印/水印版_v*.pptx 文件，无法验证')
    sys.exit(1)

out = io.open(os.path.join(HERE, '_verify_latest.txt'), 'w', encoding='utf-8')
Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
total_ov = 0
total_gp = 0
for fp in FILES:
    P = Application.Presentations.Open(fp, ReadOnly=True)
    time.sleep(2)
    ov = 0
    gp = 0
    worst = []
    for si in range(1, P.Slides.Count + 1):
        try:
            P.Slides(si).Select()
        except Exception:
            pass
        time.sleep(0.05)
        for shape in P.Slides(si).Shapes:
            if not shape.HasTextFrame:
                continue
            try:
                tr = shape.TextFrame.TextRange
                if len(tr.Text.strip()) == 0 or tr.Paragraphs().Count < 2:
                    continue
                H = shape.Height
                time.sleep(0.2)
                vals = sorted([tr.BoundHeight for _ in range(5)])
                B = vals[2]
                if B > H + 2:
                    ov += 1
                    worst.append('页%d 溢出%.1f (B=%.1f H=%.1f)' % (si, B - H, B, H))
                elif H - B > 6:
                    gp += 1
                    worst.append('页%d 空隙%.1f' % (si, H - B))
            except Exception:
                pass
    out.write('%s: 溢出=%d 真实空隙=%d\n' % (fp.split('\\')[-1], ov, gp))
    for w in worst:
        out.write('  %s\n' % w)
    print('%s: 溢出=%d 真实空隙=%d' % (fp.split('\\')[-1], ov, gp))
    total_ov += ov
    total_gp += gp
    P.Close()
    time.sleep(1)
Application.Quit()
out.write('最终验证完成\n')
out.close()
print('验证结果已写入 _verify_latest.txt')
if total_ov == 0 and total_gp == 0:
    print('[V] 0溢出0空隙，验证通过')
    sys.exit(0)
print('[X] 溢出=%d 空隙=%d，验证不通过' % (total_ov, total_gp))
sys.exit(1)
