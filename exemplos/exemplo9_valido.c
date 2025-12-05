int arr[5];
int i;

for (i = 0; i < 5; i++) {
    arr[i] = i * 2;
}

int soma = 0;
i = 0;
while (i < 5) {
    soma += arr[i];
    i++;
}

