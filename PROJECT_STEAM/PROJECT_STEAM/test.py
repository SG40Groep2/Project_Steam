import json

def get():
    with open("steam.json") as steam:
        return json.load(steam)


def merge_sort(array, left_index, right_index, optie):
    if left_index >= right_index:
        return array

    middle = (left_index + right_index)//2
    merge_sort(array, left_index, middle, optie)
    merge_sort(array, middle+1, right_index, optie)
    merge(array, left_index, right_index, middle, optie)


def merge(array, left_index, right_index, middle, optie):
    left_copy = array[left_index: middle+1]
    right_copy = array[middle+1: right_index+1]
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left_index
    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        if left_copy[left_copy_index][optie] <= right_copy[right_copy_index][optie]:
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
        sorted_index += 1
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        left_copy_index += 1
        sorted_index += 1

    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        right_copy_index += 1
        sorted_index += 1



def sort_list(lijst, optie):
    merge_sort(lijst, 0, len(lijst)-1, optie)
    return lijst


lijst = get()

name = sort_list(lijst, 'name')

def sort_a_z():
    for x in range(0,1000):
        print(name[x]['name'])

def sort_z_a():
    for x in range(1000,0 , -1):
        print(x)
        print(name[x]['name'])

sort_z_a()