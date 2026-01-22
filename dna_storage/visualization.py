import matplotlib.pyplot as plt

def visualize_mapping():
    mapping = {
        '00': 'A',
        '01': 'T',
        '10': 'C',
        '11': 'G'
    }
    
    fig, ax = plt.subplots()
    bars = ax.bar(mapping.keys(), [1]*4, color=['#4e79a7', '#59a14f', '#f28e2b', '#e15759'])
    
    ax.set_title('Binary to DNA Base Mapping')
    ax.set_ylabel('DNA Bases')
    ax.set_yticks([1]*4)
    ax.set_yticklabels(mapping.values())
    ax.set_xlabel('Binary Pairs')
    
    plt.show()

if __name__ == '__main__':
    visualize_mapping()