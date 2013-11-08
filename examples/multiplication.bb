sub cls;
    init i 50;
    while i not 0 do;
        print "";
        decr i;
    end;
end;

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

call cls;

print "Slow method:";
init X 1 + 4;
init Y 13107 * 1;
call multiply;
print "And the output is:";
print Z;

print "";

print "Sensible method:";
init X 1 + 4;
init Y 13107 * 1;
print "The output is:";
print X * Y;
