# HSV tuning log

Final thresholds:
- range1: (0,170,50) -> (7,255,255)
- range2: (173,170,50) -> (180,255,255)

Why: skin hue lives in 0-15. Saturation floor 120 let warm light push my face into the mask. Floor 170 + hue 0-7 rejects skin, keeps matte red.

Lighting tests:
- main light: red=YES face=NO
- side lamp: red=No face=YES
