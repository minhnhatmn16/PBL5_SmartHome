package com.example.smarthome;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.ListResult;
import com.google.firebase.storage.StorageReference;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

public class History extends AppCompatActivity {
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference change_history = database.getReference("change_history");

    DatabaseReference history = database.getReference("history");
    ImageButton back_main_his;
    SimpleDateFormat targetFormat = new SimpleDateFormat("dd/MM/yy HH/mm/ss");
    public String get_history(String s){
        return  s.charAt(4) + s.charAt(5) + "/" + s.charAt(2) +s.charAt(3) + "/20" + s.charAt(0) +s.charAt(1)+"  " +
                s.charAt(6) + s.charAt(7) + ":" + s.charAt(8) + s.charAt(9) +":" + s.charAt(10) +s.charAt(11);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_history);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });


        back_main_his = findViewById(R.id.back_main_his);
        back_main_his.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent  = new Intent(History.this , MainActivity.class);
                startActivity(intent);
            }
        });

        RecyclerView recyclerView = findViewById(R.id.recyclerView_his);
        List<Item_his> items = new ArrayList<>();
        MyApdapter_his apdapterHis = new MyApdapter_his(getApplicationContext(), items);


//        history.addListenerForSingleValueEvent(new ValueEventListener() {
//            @Override
//            public void onDataChange(@NonNull DataSnapshot snapshot) {
//
//            }
//
//            @Override
//            public void onCancelled(@NonNull DatabaseError error) {
//
//            }
//        });
        history.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                items.clear();
                ArrayList<Item_his> tempList = new ArrayList<>();
                for (DataSnapshot data : snapshot.getChildren()) {
                    String key = data.getKey();
                    String value = data.getValue(String.class);
                    tempList.add(new Item_his(value, get_history(key), "123", "123"));
                }
                for (int i = tempList.size() - 1; i >= 0; i--)
                    items.add(tempList.get(i));

                apdapterHis.notifyDataSetChanged();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(apdapterHis);
    }
}