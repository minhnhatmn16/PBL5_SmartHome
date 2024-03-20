package com.example.smarthome;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.SeekBar;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.firebase.Firebase;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {

    FirebaseDatabase database;
    DatabaseReference db_light;
    Integer val_light;
    ImageButton light;

    DatabaseReference db_fan;
    Integer val_fan;
    SeekBar fan;
    boolean isStart = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Get Database Firebase
        database = FirebaseDatabase.getInstance();

        db_light = database.getReference("light");
        light = findViewById(R.id.image_light);

        db_fan = database.getReference("fan");
        fan = findViewById(R.id.fan);


        db_light.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                val_light = snapshot.getValue(Integer.class);
                if (val_light == 0) {
                    light.setBackgroundResource(R.drawable.off);
                } else {
                    light.setBackgroundResource(R.drawable.on);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

        db_fan.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                val_fan = snapshot.getValue(Integer.class);
                if (!isStart) {
                    fan.setProgress(val_fan);
                    isStart = true;
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });


        light.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (val_light == 0) {
                    val_light = 1;
                    light.setBackgroundResource(R.drawable.on);
                    db_light.setValue(val_light);
                } else {
                    val_light = 0;
                    light.setBackgroundResource(R.drawable.off);
                    db_light.setValue(val_light);
                }
            }
        });


        fan.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                val_fan = progress;
                db_fan.setValue(val_fan);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });
    }


}