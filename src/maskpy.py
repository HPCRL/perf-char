import sys

def generate_masks_recursively(dims, mask, chosen_dims, masks, index=0):
    if index == len(chosen_dims):
        masks.append(mask.copy())
        return

    mask[chosen_dims[index]] = -1
    generate_masks_recursively(dims, mask, chosen_dims, masks, index + 1)

    mask[chosen_dims[index]] = 1
    generate_masks_recursively(dims, mask, chosen_dims, masks, index + 1)

def generate_masks(dims, chosen_dims, masks):
    mask = [0] * dims
    generate_masks_recursively(dims, mask, chosen_dims, masks)

def get_remaining_dims(total_dims, exclude_dims):
    remaining_dims = [i for i in range(total_dims) if i not in exclude_dims]
    return remaining_dims

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <total_dims> <num_hops>")
        sys.exit(1)

    total_dims = int(sys.argv[1])
    num_hops = int(sys.argv[2])

    exclude_dims = []

    remaining_dims = get_remaining_dims(total_dims, exclude_dims)

    dimensions = [0] * len(remaining_dims)
    dimensions[-num_hops:] = [1] * num_hops

    masks = []

    while True:
        chosen_dims = [remaining_dims[i] for i in range(len(remaining_dims)) if dimensions[i] == 1]
        generate_masks(total_dims, chosen_dims, masks)

        next_permutation_possible = False
        for i in range(len(dimensions) - 1, 0, -1):
            if dimensions[i - 1] < dimensions[i]:
                next_permutation_possible = True
                break

        if not next_permutation_possible:
            break

        j = len(dimensions) - 1
        while dimensions[j - 1] >= dimensions[j]:
            j -= 1

        dimensions[j - 1], dimensions[j:] = dimensions[j - 1], sorted(dimensions[j:])
        
    for mask in masks:
        print(','.join(map(str, mask)))

    print("Total masks:", len(masks))
