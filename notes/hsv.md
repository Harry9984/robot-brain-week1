# HSV tuning log

current best thresholds:
- range1: (0,170,50) -> (7,255,255)
- range2: (173,170,50) -> (180,255,255)

Why: skin hue lives in 0-15. Saturation floor 120 let warm light push my face into the mask. Floor 170 + hue 0-7 rejects skin, keeps matte red.

Lighting tests:
- main light: red=YES face=NO
- side lamp: red=No face=YES

Update: Saturation floor raised to 195.
Discovered the difference between emitting light (phone screen) and reflecting light (real objects). Phone screens are highly saturated, making them easy to detect. Real objects scatter ambient room light, lowering saturation and mixing colors. Color alone is a weak feature in the real world.
