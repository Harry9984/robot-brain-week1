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

The Limit of HSV:
Raised saturation to 195 to reject orange. This shattered real-world 3D objects into fragmented pieces because physical reflections drop below 195 saturation. Morphological closing (21x21 kernel) failed to bridge the massive gaps. Lowered back to 160 and raised area threshold to 2000. 
Conclusion: Pure color thresholding is a toy technique. It fails on 3D objects under mixed ambient light. Future upgrades must use shape/texture (Neural Networks).

BUSINESS LOG - PLATFORM RISK:
Upwork consumed all 35 Connects as an ID verification fee.
Lesson 1: Sunk cost. Do not mourn, do not re-buy from food money.
Lesson 2: Never depend on one platform. Open zero-cost channels (Fiverr, Reddit).
Lesson 3: Reload rule - Connects only from surplus, $5.25 custom amount, never $15 default.
