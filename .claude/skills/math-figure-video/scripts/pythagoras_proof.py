"""Euclid's proof of the Pythagorean theorem (shearing / bride's chair).

Beat sheet:
  1) figure: right triangle ABC, squares on all sides, altitude C->J->K
  2) LEFT set  : ACE -> EAB -> CAF -> AFJ  (each replaces previous), keep #1 & #4
  3) RIGHT set : BCH -> BHA -> CBG -> JBG  (same), keep #1 & #4
  4) fill ACDE + AFKJ green, BHIC + JKGB pink, "넓이가 같다" captions
"""
import numpy as np
from manim import *

KOR = "Noto Sans CJK KR"

# ---- original coordinates (right angle at C; altitude foot J on AB, K on FG) ----
_A=[0,0,0]; _B=[4,0,0]; _C=[2.4,1.96,0]
_F=[0,-4,0]; _G=[4,-4,0]; _J=[2.4,0,0]; _K=[2.4,-4,0]
_E=[-1.96,2.4,0]; _D=[0.44,4.36,0]; _H=[5.96,1.6,0]; _I=[4.36,3.56,0]

CENTER = np.array([2.0, 0.18, 0.0]); S = 0.82
def P(p): return (np.array(p, float) - CENTER) * S
A,B,C,F,G,J,K,E,D,H,I = map(P,[_A,_B,_C,_F,_G,_J,_K,_E,_D,_H,_I])

GREEN_F="#BFE3C0"; GREEN_S="#3F8A4E"; PINK_F="#F6C9D8"; PINK_S="#C4547F"
INK="#2A2A2A"; PURPLE="#9C3FA0"

def tri(p,q,r,color):
    return Polygon(p,q,r,color=color,stroke_width=3,fill_color=color,fill_opacity=0.5)


class Pyth(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # ---------- PHASE 1: figure ----------
        triangle = Polygon(A,B,C,color=INK,stroke_width=6)
        sq_AB = Polygon(A,B,G,F,color=INK,stroke_width=4)
        sq_AC = Polygon(A,C,D,E,color=GREEN_S,stroke_width=4)
        sq_BC = Polygon(B,H,I,C,color=PINK_S,stroke_width=4)
        alt = Line(C,K,color=INK,stroke_width=3)
        ra_C = RightAngle(Line(C,A),Line(C,B),length=0.22,color=INK)
        ra_K = RightAngle(Line(K,J),Line(K,G),length=0.22,color=INK)

        labels = VGroup()
        for pt,name,d in [(A,"A",DL),(B,"B",DR),(C,"C",UP),(D,"D",UP),(E,"E",LEFT),
                          (F,"F",DL),(G,"G",DR),(H,"H",RIGHT),(I,"I",UR),
                          (J,"J",UL),(K,"K",DOWN)]:
            labels.add(Text(name,font=KOR,color=INK,weight=BOLD).scale(0.5).next_to(pt,d,buff=0.1))

        self.play(Create(triangle),run_time=1.2)
        self.play(Create(ra_C),run_time=0.4)
        self.play(Create(sq_AC),Create(sq_BC),Create(sq_AB),run_time=1.6)
        self.play(Create(alt),Create(ra_K),run_time=0.8)
        self.play(FadeIn(labels,lag_ratio=0.15),run_time=1.2)
        self.wait(0.6)

        # ---------- PHASE 2: LEFT set ----------
        L = [tri(A,C,E,GREEN_S),tri(E,A,B,GREEN_S),tri(C,A,F,GREEN_S),tri(A,F,J,GREEN_S)]
        self.play(FadeIn(L[0]),run_time=0.7); self.wait(0.5)
        cur = L[0].copy(); self.add(cur)
        for nxt in L[1:]:
            self.play(Transform(cur,nxt),run_time=1.0); self.wait(0.5)
        keepL = L[0].copy(); self.play(FadeIn(keepL),run_time=0.6); self.wait(0.8)

        # ---------- PHASE 3: RIGHT set ----------
        R = [tri(B,C,H,PINK_S),tri(B,H,A,PINK_S),tri(C,B,G,PINK_S),tri(J,B,G,PINK_S)]
        self.play(FadeIn(R[0]),run_time=0.7); self.wait(0.5)
        curR = R[0].copy(); self.add(curR)
        for nxt in R[1:]:
            self.play(Transform(curR,nxt),run_time=1.0); self.wait(0.5)
        keepR = R[0].copy(); self.play(FadeIn(keepR),run_time=0.6); self.wait(0.8)

        self.play(FadeOut(cur),FadeOut(keepL),FadeOut(L[0]),
                  FadeOut(curR),FadeOut(keepR),FadeOut(R[0]),run_time=0.6)

        # ---------- PHASE 4: fill ----------
        f_AC   = Polygon(A,C,D,E).set_fill(GREEN_F,0.85).set_stroke(GREEN_S,4)
        f_AFKJ = Polygon(A,F,K,J).set_fill(GREEN_F,0.85).set_stroke(GREEN_S,4)
        f_BC   = Polygon(B,H,I,C).set_fill(PINK_F,0.85).set_stroke(PINK_S,4)
        f_JKGB = Polygon(J,K,G,B).set_fill(PINK_F,0.85).set_stroke(PINK_S,4)
        self.play(FadeIn(f_AC),FadeIn(f_AFKJ),run_time=1.0)
        self.play(FadeIn(f_BC),FadeIn(f_JKGB),run_time=1.0)
        self.add(labels)
        self.wait(0.4)

        capL = Text("넓이가 같다",font=KOR,color=PURPLE,weight=BOLD).scale(0.5).to_edge(LEFT).shift(DOWN*1.2)
        capR = Text("넓이가 같다",font=KOR,color=PURPLE,weight=BOLD).scale(0.5).to_edge(RIGHT).shift(DOWN*1.2)
        aL = Arrow(capL.get_right(), Polygon(A,F,K,J).get_center(), color=PURPLE, stroke_width=4, buff=0.15)
        aR = Arrow(capR.get_left(), Polygon(J,K,G,B).get_center(), color=PURPLE, stroke_width=4, buff=0.15)
        self.play(FadeIn(capL),FadeIn(capR),GrowArrow(aL),GrowArrow(aR),run_time=1.0)
        self.wait(1.5)
