#include<stdio.h>
int main(){
    float sum,diff, mul,div;
    float a,b;
    float choice;
    printf("1. Addition Of 2 Numbers \n");
    printf("2. Subtraction Of 2 Numbers \n");
    printf("3. Multiplication Of 2 Numbers \n");
    printf("4. Division Of 2 Numbers \n");

    printf("Enter The Choice: ");
    scanf("%f", &choice);

    if (choice == 1){
        printf("Enter 1st Number: ");
        scanf("%f",&a);
        printf("Enter 2nd Number: ");
        scanf("%f",&b);
        sum = a + b;
        printf("The Sum Is : %f", sum);
    }
    else if (choice == 2){
        printf("Enter 1st Number: ");
        scanf("%f", &a);
        printf("Enter 2nd Number: ");
        scanf("%f",&b);
        diff = a - b;
        printf("The Sum Is : %f", diff);
    }
    else if (choice == 3){
        printf("Enter 1st Number: ");
        scanf("%f",&a);
        printf("Enter 2nd Number: ");
        scanf("%f",&b);
        mul = a * b;
        printf("The Multiplication Is : %f", mul);
    }
    else if (choice == 4){
        printf("Enter 1st Number: ");
        scanf("%f",&a);
        printf("Enter 2nd Number: ");
        scanf("%f",&b);
        div = a / b;
        printf("The Division Is : %f", div);
    }
    else{
        printf("Enter Valid Choice");
    }
}



