from backend.utils import StegnoGen

s = StegnoGen()
s.generate_random_image(512,512,3,"output/randomgen.png")
s.embed_string_to_image("Hi this is a test string","password123","output/test.png")

s.read_image("output/test.png")
print(s.extract_text_from_image("password123"))