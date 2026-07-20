"""Euclid Pythagorean proof — split into 5 scenes, white or transparent bg.

Scenes:
  Phase1  도형 준비        (figure builds from scratch)
  Phase2  왼쪽 세트        (figure static + left shear:  ACE->EAB->CAF->AFJ)
  Phase3  오른쪽 세트      (figure static + right shear: BCH->BHA->CBG->JBG)
  Phase4  색칠             (figure static + fill ACDE/AFKJ green, BHIC/JKGB pink)
  Full    통합본           (all four in sequence)

Background: white by default; set env TRANSPARENT=1 and render with -t for alpha.
"""
import os
import numpy as np
from manim import *

KOR = "Noto Sans CJK KR"
TRANSPARENT = bool(os.environ.get("TRANSPARENT"))

_A=[0,0,0]; _B=[4,0,0]; _C=[2.4,1.96,0]
_F=[0,-4,0]; _G=[4,-4,0]; _J=[2.4,0,0]; _K=[2.4,-4,0]
_E=[-1.96,2.4,0]; _D=[0.44,4.36,0]; _H=[5.96,1.6,0]; _I=[4.36,3.56,0]
CENTER = np.array([2.0, 0.18, 0.0]); S = 0.82
def P(p): return (np.array(p, float) - CENTER) * S
A,B,C,F,G,J,K,E,D,H,I = map(P,[_A,_B,_C,_F,_G,_J,_K,_E,_D,_H,_I])

GREEN_F="#BFE3C0"; GREEN_S="#3F8A4E"; PINK_F="#F6C9D8"; PINK_S="#C4547F"
INK="#2A2A2A"; PURPLE="#9C3FA0"

def tri(p,q,r,c): return Polygon(p,q,r,color=c,stroke_width=3,fill_color=c,fill_opacity=0.5)

def figure_parts():
    return dict(
        triangle=Polygon(A,B,C,color=INK,stroke_width=6),
        sq_AB=Polygon(A,B,G,F,color=INK,stroke_width=4),
        sq_AC=Polygon(A,C,D,E,color=GREEN_S,stroke_width=4),
        sq_BC=Polygon(B,H,I,C,color=PINK_S,stroke_width=4),
        alt=Line(C,K,color=INK,stroke_width=3),
        ra_C=RightAngle(Line(C,A),Line(C,B),length=0.22,color=INK),
        ra_K=RightAngle(Line(K,J),Line(K,G),length=0.22,color=INK),
    )

def make_labels():
    g=VGroup()
    for pt,name,d in [(A,"A",DL),(B,"B",DR),(C,"C",UP),(D,"D",UP),(E,"E",LEFT),
                      (F,"F",DL),(G,"G",DR),(H,"H",RIGHT),(I,"I",UR),(J,"J",UL),(K,"K",DOWN)]:
        g.add(Text(name,font=KOR,color=INK,weight=BOLD).scale(0.5).next_to(pt,d,buff=0.1))
    return g

def left_tris():  return [tri(A,C,E,GREEN_S),tri(E,A,B,GREEN_S),tri(C,A,F,GREEN_S),tri(A,F,J,GREEN_S)]
def right_tris(): return [tri(B,C,H,PINK_S),tri(B,H,A,PINK_S),tri(C,B,G,PINK_S),tri(J,B,G,PINK_S)]


class _Base(Scene):
    def bg(self):
        if not TRANSPARENT:
            self.camera.background_color = WHITE

    def add_figure_static(self):
        parts = figure_parts(); labels = make_labels()
        self.add(*parts.values(), labels)
        return parts, labels

    def build_figure_anim(self):
        p = figure_parts(); labels = make_labels()
        self.play(Create(p["triangle"]),run_time=1.2)
        self.play(Create(p["ra_C"]),run_time=0.4)
        self.play(Create(p["sq_AC"]),Create(p["sq_BC"]),Create(p["sq_AB"]),run_time=1.6)
        self.play(Create(p["alt"]),Create(p["ra_K"]),run_time=0.8)
        self.play(FadeIn(labels,lag_ratio=0.15),run_time=1.2)
        return p, labels

    def play_set(self, tris):
        self.play(FadeIn(tris[0]),run_time=0.7); self.wait(0.5)
        cur = tris[0].copy(); self.add(cur)
        for nxt in tris[1:]:
            self.play(Transform(cur,nxt),run_time=1.0); self.wait(0.5)
        keep = tris[0].copy(); self.play(FadeIn(keep),run_time=0.6); self.wait(0.8)
        return cur, keep

    def play_fills(self, with_captions=True):
        fills = VGroup(
            Polygon(A,C,D,E).set_fill(GREEN_F,0.85).set_stroke(GREEN_S,4),
            Polygon(A,F,K,J).set_fill(GREEN_F,0.85).set_stroke(GREEN_S,4),
            Polygon(B,H,I,C).set_fill(PINK_F,0.85).set_stroke(PINK_S,4),
            Polygon(J,K,G,B).set_fill(PINK_F,0.85).set_stroke(PINK_S,4),
        )
        self.play(FadeIn(fills[0]),FadeIn(fills[1]),run_time=1.0)
        self.play(FadeIn(fills[2]),FadeIn(fills[3]),run_time=1.0)
        self.add(make_labels())
        self.wait(0.4)
        if with_captions:
            capL = Text("넓이가 같다",font=KOR,color=PURPLE,weight=BOLD).scale(0.5).to_edge(LEFT).shift(DOWN*1.2)
            capR = Text("넓이가 같다",font=KOR,color=PURPLE,weight=BOLD).scale(0.5).to_edge(RIGHT).shift(DOWN*1.2)
            aL = Arrow(capL.get_right(),Polygon(A,F,K,J).get_center(),color=PURPLE,stroke_width=4,buff=0.15)
            aR = Arrow(capR.get_left(),Polygon(J,K,G,B).get_center(),color=PURPLE,stroke_width=4,buff=0.15)
            self.play(FadeIn(capL),FadeIn(capR),GrowArrow(aL),GrowArrow(aR),run_time=1.0)
        self.wait(1.5)


class Phase1(_Base):
    def construct(self):
        self.bg(); self.build_figure_anim(); self.wait(0.8)

class Phase2(_Base):
    def construct(self):
        self.bg(); self.add_figure_static(); self.wait(0.4); self.play_set(left_tris())

class Phase3(_Base):
    def construct(self):
        self.bg(); self.add_figure_static(); self.wait(0.4); self.play_set(right_tris())

class Phase4(_Base):
    def construct(self):
        self.bg(); self.add_figure_static(); self.wait(0.4); self.play_fills()

class Full(_Base):
    def construct(self):
        self.bg()
        self.build_figure_anim(); self.wait(0.6)
        L=left_tris();  curL,keepL = self.play_set(L)
        R=right_tris(); curR,keepR = self.play_set(R)
        self.play(FadeOut(curL),FadeOut(keepL),FadeOut(L[0]),
                  FadeOut(curR),FadeOut(keepR),FadeOut(R[0]),run_time=0.6)
        self.play_fills()

# backward-compat alias
class Pyth(Full):
    pass
