sub multiply;
    print "Your input was:";
    print X;
    print Y;

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

init X 1 + 4;
init Y 13107;
call multiply;

print "";
print "And the output is:";
print Z;
