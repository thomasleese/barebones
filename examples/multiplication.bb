sub multiply;
    if X == 5 then;
        if Y == 13107 then;
            print "HELLO";
        end;
    end;

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
end;

init X 5;
init Y 13107;
call multiply;
