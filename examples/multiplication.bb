clear X;
incr X;
incr X;
clear Y;
incr Y;
incr Y;
incr Y;
clear Z;

while X not 0 do;
    clear W;
    
    while Y not 0 do;
        incr Z;
        incr W;
        decr Y;
    end;

    while W not 0 do;
        incr Y;
        decr W;
    end;

    decr X;
end;

