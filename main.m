global TOTAL;
TOTAL = 10;
n = [34, 45, 25, 45, 33, 19, 40, 34, 38, 42];
av = average(n)


function avg = average(nums)
global TOTAL
avg = sum(nums)/TOTAL;
end