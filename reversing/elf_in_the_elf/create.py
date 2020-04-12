from pwn import *

inner = open("inner", "rb").read()
inner = [char for char in inner]
template = open("template.c", "rb").read()

operations = ['+', '-', '^']

for i in range(0, len(inner)):
	filename = "elfs/elf_" + str(i) + ".c"
	file_contents = template
	op = operations[randint(0,2)]
	constant = randint(0,255)

	file_contents = file_contents.replace("operation", op, 1)
	file_contents = file_contents.replace("constant", str(constant), 1)
	if op == '+':
		solution = ((ord(inner[i]) + constant) & 0xff)
	elif op == '-':
		solution = ((ord(inner[i]) - constant) & 0xff)
	else:
		solution = ((ord(inner[i]) ^ constant) & 0xff)
	file_contents = file_contents.replace("solution", str(solution), 1)

	open(filename, "wb").write(file_contents)
	execute = "gcc " + filename + " -o " + filename.split(".c",1)[0]
	os.system(execute)
