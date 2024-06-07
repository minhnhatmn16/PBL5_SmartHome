package com.example.smarthome;

import android.app.Dialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.CompoundButton;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.Toast;

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
    DatabaseReference history = database.getReference("history");
    DatabaseReference door = database.getReference("door");
    DatabaseReference rheostat = database.getReference("rheostat");

    int val_rheostat;
    Switch switch_door;
    ImageButton back_main_his;
    SimpleDateFormat targetFormat = new SimpleDateFormat("dd/MM/yy HH/mm/ss");
    public boolean check(String s){
        return s.contains(Character.toString('~'));
    }
    public String get_time(String s){
        String year = "20" + s.substring(0,2);
        String month = s.substring(2,4);
        String day = s.substring(4,6);
        String hour = s.substring(6,8);
        String minute = s.substring(8,10);
        String second = s.substring(10,12);
        return day + "/" + month + "/" + year + " " + hour + ":" + minute + ":" + second;
    }
    public String get_id(String s){
        return s.split("~")[1];
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

        switch_door = findViewById(R.id.switch_door);
        door.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                int val_door = snapshot.getValue(Integer.class);
                if (val_door == 1){
                    switch_door.setChecked(true);
                } else {
                    switch_door.setChecked(false);
                }
            }
            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
        rheostat.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                val_rheostat = snapshot.getValue(Integer.class);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
        switch_door.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                switch_door.setChecked(true);
//                door.setValue(1);

//                switch_door.setOnCheckedChangeListener((button, isChecked) ->{
//                    if (isChecked == false) {
//                        if (val_rheostat > 50) {
//                            switch_door.setChecked(true);
//                            Toast.makeText(History.this,"The door is not closed yet", Toast.LENGTH_SHORT).show();
//                        } else {
//                            door.setValue(0);
//                        }
//                    } else {
//                        door.setValue(1);
//                    }
//                });




            }
        });
        switch_door.setOnCheckedChangeListener((button, isChecked) ->{
            if (isChecked == false) {
                if (val_rheostat > 50) {
                    switch_door.setChecked(true);
                    Toast.makeText(History.this,"The door is not closed yet", Toast.LENGTH_SHORT).show();
                } else {
                    door.setValue(0);
                }
            } else {
                door.setValue(1);
            }
        });


        RecyclerView recyclerView = findViewById(R.id.recyclerView_his);
        List<Item_his> items = new ArrayList<>();
        MyApdapter_his apdapterHis = new MyApdapter_his(getApplicationContext(), items);
        history.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                items.clear();
                ArrayList<Item_his> tempList = new ArrayList<>();
                for (DataSnapshot data : snapshot.getChildren()) {
                    String key = data.getKey();
                    String value = data.getValue(String.class);
                    if (check(value)){
                        tempList.add(new Item_his( value.split("~")[0], get_time(key), key, value.split("~")[1]));
                    } else {
                        tempList.add(new Item_his( value, get_time(key), "",""));
                    }
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
        apdapterHis.setListener(new MyApdapter_his.OnItemClickListener() {
            @Override
            public void onItemClick(Item_his item) {
                if (item.getImageUrl() != "")
                    showImageDialog(item.getImageUrl()+".jpg");
            }
        });
    }

    public void showImageDialog(String imageName) {
        // Tạo dialog để hiển thị hình ảnh
        final Dialog dialog = new Dialog(History.this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.dialog_image);

        // Lấy ImageView từ layout dialog
        ImageView dialogImageView = dialog.findViewById(R.id.dialog_image_view);

        // Tạo một StorageReference từ Firebase Storage
        FirebaseStorage storage = FirebaseStorage.getInstance();
        StorageReference storageHistoryRef = storage.getReference().child("history");
        StorageReference imageRef = storageHistoryRef.child(imageName);

        // Tải hình ảnh từ Firebase Storage và hiển thị vào ImageView
        imageRef.getBytes(Long.MAX_VALUE).addOnSuccessListener(new OnSuccessListener<byte[]>() {
            @Override
            public void onSuccess(byte[] bytes) {
                Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                dialogImageView.setImageBitmap(bitmap);
            }

        });

        // Đặt kích thước hình ảnh
        ViewGroup.LayoutParams layoutParams = dialogImageView.getLayoutParams();
        layoutParams.width = dpToPx(300);
        layoutParams.height = dpToPx(300);

        // Close dialog khi bấm ra ngoài hình ảnh
        dialog.setCanceledOnTouchOutside(true);

        // Hiển thị dialog
        dialog.show();
    }

    public int dpToPx(int dp) {
        float density = getResources().getDisplayMetrics().density;
        return Math.round((float) dp * density);
    }
}

