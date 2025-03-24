from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

p = pipeline(
    Tasks.named_entity_recognition,
    
    # preprocessor = '/root/cjr/projects/adaseq/adaseq/pretrained-models/distilbert',
    '/root/cjr/figure/250214005303.842435/output_best'
)
result = p('quite, serene, clean, a lot of trees with flowers, nice to spend quite time here to relax.')

print(result)

# # p = pipeline(
# #     Tasks.named_entity_recognition,
# #     'damo/nlp_raner_named-entity-recognition_chinese-base-resume'  # model_id
# # )
# # result = p('1984年出生，中国国籍，汉族，硕士学历')

# # print(result)
# # {'output': [{'type': 'CONT', 'start': 8, 'end': 12, 'span': '中国国籍'}, {'type': 'RACE', 'start': 13, 'end': 15, 'span': '汉族'}, {'type': 'EDU', 'start': 16, 'end': 20, 'span': '硕士学历'}]}
