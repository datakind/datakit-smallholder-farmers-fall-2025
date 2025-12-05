UPDATE questions_deduped
SET question_topic = regexp_replace(question_topic,  '^,?["'']+|["'']+$', '');

UPDATE questions_deduped
SET question_topic = regexp_replace(question_topic, '^,"|"$', '');

ALTER TABLE questions_deduped ADD COLUMN question_topic_clean VARCHAR;

UPDATE questions_deduped
SET question_topic_clean = regexp_extract(
    lower(question_topic),
    '(cow|goat|sheep|pig|hen|chicken|turkey|duck|rabbit|fish|tilapia|catfish|maize|corn|bean|cassava|tomato|cabbage|sukuma|pepper|onion|rice|banana|sweet potato|potato|watermelon|carrot|coffee|tea|millet|sorghum|groundnut|soybean|animal|aubergine|cocoa|butternut-squash|leek|snap-pea|birds|chicks|avocado|bamboo|bee|cucumber|amaranth|lupin|gooseberry|asparagus|black[- ]?nightshade|milk|cranberry|grass|mushroom|beetroot|taro|rapeseed|chilli|snow[- ]?pea|oat|coconut|cereal crops?|passion fruits?|crop|kale|peanut|sugar[- ]?cane|cotton|courgette|orange|guinea[- ]?fowl|blackberry|pumpkin|napier[- ]?grass|sisal|pineapple|jackfruit|chia|broccoli|ostrich|leucaena|dairy|mangada|cattle|kales?|soya|garlic|passion[- ]?fruit|mango|pyrethrum|greens|grape|guava|pea|cat|clover|dog|apple|lemon|okra|sesame|rye|celery|flower|paw[- ]?paw|capsicum|lettuce|sudan[- ]?grass|acacia|brand|livestock|yam|eucalyptus|pear|peach|plant|sunflower|bird|flax|parsley|poultry|ginger|vegetable|radish|cashcrop|vetch|spinach|tobacco leaves|tobacco|cashew[- ]?nut|safflower|apricot|olive|boma[- ]?rhodes|cyprus|squash|cauliflower|wheat|collard[- ]?greens|camel|plantain|locust|coriander|setaria|barley|mulberry|macadamia|miraa|cereal|melon|strawberry|african[- ]?nightshade|nightshade|brachiaria[- ]?grass|chickpea)'
);
