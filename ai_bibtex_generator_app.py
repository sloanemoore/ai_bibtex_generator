from openai import OpenAI
from config import API_KEY


client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are an expert Japanese to English translator."},
    {"role": "user", "content": "Please translate the following Japanese text to English: 人間が妖精を使役する、ハイランド王国。 王都ルイストンでは毎年秋に、王家主催の砂糖菓子品評会が開催されていた。 品評会で最高位の王家勲章を勝ち取った者は、「銀砂糖師」を名乗ることが許される。 少女・アンは、亡き母の職業であった「銀砂糖師」になるため、ルイストンへ向かうことに。 道中の用心棒として雇った戦士妖精・シャルは口が悪く、無愛想で一筋縄ではいかない。 果たしてアンは、無事ルイストンにたどり着き「銀砂糖師」になることができるのか!? 人間と妖精が形創る、甘くて美しいおとぎ話、開幕。 巻末には原作者、三川みり書き下ろし短編を収録。."}
  ]
)

print(completion.choices[0].message)