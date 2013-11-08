sub cls;
    init i 50;
    while i not 0 do;
        print "";
        decr i;
    end;
end;

sub show_input;
    print "Your input was:";
    print X;
    print Y;
end;

sub show_output;
    print "And the output was:";
    print Z;
end;

sub slow_multiply;
    print "Slow method:";
    call show_input;

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

    call show_output;
end;

sub sensible_multiply;
    print "Sensible method:";
    call show_input;
    
    init Z X * Y;

    call show_output;
end;

call cls;

init X 1 + 4;
init Y 13107 * 1;
call slow_multiply;

print "";

init X 1 + 4;
init Y 13107 * 1;
call sensible_multiply;
